"""Tests for lib.telegram_publisher — Telegram Bot API push (Phase G T12 + T14b)."""
import json
from unittest.mock import patch, MagicMock
from pathlib import Path
import pytest

from lib.telegram_publisher import TelegramPublisher, load_telegram_config, _md_to_telegram_html


def test_publisher_init():
    p = TelegramPublisher("token123", "chat-1", "http://localhost:5174/")
    assert p.bot_token == "token123"
    assert p.chat_id == "chat-1"
    assert p.base_url == "http://localhost:5174"  # trailing slash stripped
    assert p.linked_group_chat_id is None  # T14b — optional, default None


def test_publisher_init_with_linked_group():
    p = TelegramPublisher("t", "c", "http://x", linked_group_chat_id="g-1")
    assert p.linked_group_chat_id == "g-1"


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
    assert pub.linked_group_chat_id is None  # not provided → None


def test_load_config_with_linked_group(tmp_path):
    """T14b — linked_group_chat_id field optional, populated when present."""
    p = tmp_path / "secrets.yaml"
    p.write_text(
        "telegram:\n  bot_token: tk\n  chat_id: c1\n  base_url: http://x\n"
        "  linked_group_chat_id: g-1\n"
    )
    pub = load_telegram_config(p)
    assert pub is not None
    assert pub.linked_group_chat_id == "g-1"


# ===== T14b — Markdown → Telegram HTML conversion =====


def test_md_to_html_bold():
    assert _md_to_telegram_html("**bold**") == "<b>bold</b>"
    assert _md_to_telegram_html("Plain **bold** text") == "Plain <b>bold</b> text"


def test_md_to_html_bullets():
    """`- item` lines → `• item` (Telegram doesn't support <ul>)."""
    md = "- First\n- Second\n- Third"
    expected = "• First\n• Second\n• Third"
    assert _md_to_telegram_html(md) == expected


def test_md_to_html_bullet_with_bold():
    """Master pattern: `- **highlight**: text` → `• <b>highlight</b>: text`."""
    md = "- **Highlight**: detail text"
    expected = "• <b>Highlight</b>: detail text"
    assert _md_to_telegram_html(md) == expected


def test_md_to_html_h2_heading():
    """`## Heading` → `<b>Heading</b>` (Telegram has no native h2)."""
    assert _md_to_telegram_html("## Góc nhìn ngược") == "<b>Góc nhìn ngược</b>"
    assert _md_to_telegram_html("### Sub heading") == "<b>Sub heading</b>"


def test_md_to_html_full_master_body():
    """Realistic Master body with paragraph + bullets + closing."""
    md = """BIDV mở đầu 2026 với kết quả tài chính hai mặt.

- **Thu nhập tăng**: lợi nhuận trước thuế 8.572 tỷ
- **Nợ xấu cao**: tỷ lệ 1,76%

Phù hợp NĐT giá trị giữ trên 12 tháng."""
    out = _md_to_telegram_html(md)
    assert "• <b>Thu nhập tăng</b>: lợi nhuận trước thuế 8.572 tỷ" in out
    assert "• <b>Nợ xấu cao</b>: tỷ lệ 1,76%" in out
    assert "Phù hợp NĐT giá trị" in out
    assert "**" not in out  # all bold converted
    assert "- " not in out.replace("- thuế", "")  # bullets converted (allow words containing dash)


# ===== T14b — publish_article_with_thread_body =====


def _mock_urlopen_factory(responses: list[dict]):
    """Build a mock urlopen that returns each response in order, then raises StopIteration if exhausted."""
    iter_responses = iter(responses)

    def _build(*_args, **_kwargs):
        next_resp = next(iter_responses)
        m = MagicMock()
        m.read.return_value = json.dumps(next_resp).encode("utf-8")
        m.__enter__ = lambda self: self
        m.__exit__ = lambda *args: None
        return m

    return _build


def test_thread_publish_no_linked_group_falls_back_to_legacy():
    """linked_group_chat_id None → publish_article_with_thread_body() delegates to publish_article()."""
    p = TelegramPublisher("t", "c", "http://x", linked_group_chat_id=None)
    responses = [
        {"ok": True, "result": {"message_id": 99}},
    ]
    with patch("lib.telegram_publisher.urllib.request.urlopen",
               side_effect=_mock_urlopen_factory(responses)):
        result = p.publish_article_with_thread_body("T", "body **md**", "slug")
    assert result["status"] == "pushed"
    assert result["telegram_message_id"] == 99
    assert "thread_message_id" not in result  # legacy shape


def test_thread_publish_full_flow_success():
    """T14b happy path: drain → channel post → 1 poll → reply in thread."""
    p = TelegramPublisher("t", "c", "http://x", linked_group_chat_id="g-1")
    responses = [
        # _drain_offset: getUpdates (no stale)
        {"ok": True, "result": []},
        # Channel post sendMessage
        {"ok": True, "result": {"message_id": 100}},
        # _wait_for_auto_forward: getUpdates returns auto-forward
        {"ok": True, "result": [{
            "update_id": 1,
            "message": {
                "message_id": 200,
                "chat": {"id": "g-1"},
                "is_automatic_forward": True,
                "forward_from_message_id": 100,
            },
        }]},
        # Thread reply sendMessage
        {"ok": True, "result": {"message_id": 201}},
    ]
    with patch("lib.telegram_publisher.time.sleep"):  # speed up poll loop
        with patch("lib.telegram_publisher.urllib.request.urlopen",
                   side_effect=_mock_urlopen_factory(responses)):
            result = p.publish_article_with_thread_body("Title", "Body", "slug")
    assert result["status"] == "pushed"
    assert result["telegram_message_id"] == 100
    assert result["thread_message_id"] == 200
    assert result["body_message_id"] == 201
    assert result["error"] is None


def test_thread_publish_no_thread_detected():
    """Auto-forward never appears in poll window → status=pushed_no_thread (channel OK, body skipped)."""
    p = TelegramPublisher("t", "c", "http://x", linked_group_chat_id="g-1")
    # Drain returns empty, channel post succeeds, then 8 empty polls
    responses = [
        {"ok": True, "result": []},
        {"ok": True, "result": {"message_id": 100}},
    ] + [{"ok": True, "result": []} for _ in range(8)]
    with patch("lib.telegram_publisher.time.sleep"):
        with patch("lib.telegram_publisher.urllib.request.urlopen",
                   side_effect=_mock_urlopen_factory(responses)):
            result = p.publish_article_with_thread_body(
                "Title", "Body", "slug",
                max_poll_attempts=8, poll_interval_sec=0,
            )
    assert result["status"] == "pushed_no_thread"
    assert result["telegram_message_id"] == 100
    assert result["thread_message_id"] is None
    assert result["body_message_id"] is None
    assert "auto-forward not detected" in result["error"]


def test_thread_publish_channel_post_fails():
    """Channel post itself fails → status=failed (no thread attempt)."""
    p = TelegramPublisher("t", "c", "http://x", linked_group_chat_id="g-1")
    responses = [
        {"ok": True, "result": []},  # drain
        {"ok": False, "description": "Bot blocked"},  # channel post fail
    ]
    with patch("lib.telegram_publisher.urllib.request.urlopen",
               side_effect=_mock_urlopen_factory(responses)):
        result = p.publish_article_with_thread_body("T", "B", "s")
    assert result["status"] == "failed"
    assert result["telegram_message_id"] is None
    assert "Bot blocked" in result["error"]
