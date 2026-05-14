"""Tests for lib.telegram_publisher — Telegram Bot API push (Phase G T12 + T14b)."""
import json
from unittest.mock import patch, MagicMock
from pathlib import Path
import pytest

from datetime import datetime, timezone, timedelta

from lib.telegram_publisher import (
    TelegramPublisher,
    load_telegram_config,
    _md_to_telegram_html,
    _format_duration,
    _format_tokens,
    _build_channel_text,
)


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
    """T14b happy path: drain → channel post (3 lines) → 1 poll → 2 thread replies (body + link)."""
    p = TelegramPublisher("t", "c", "http://x", linked_group_chat_id="g-1")
    responses = [
        # _drain_offset: getUpdates (no stale)
        {"ok": True, "result": []},
        # Channel post sendMessage (3 lines)
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
        # Thread reply 1 — body
        {"ok": True, "result": {"message_id": 201}},
        # Thread reply 2 — link
        {"ok": True, "result": {"message_id": 202}},
    ]
    with patch("lib.telegram_publisher.time.sleep"):
        with patch("lib.telegram_publisher.urllib.request.urlopen",
                   side_effect=_mock_urlopen_factory(responses)):
            result = p.publish_article_with_thread_body(
                "Title", "Body", "slug",
                write_duration_ms=204000,
                tokens=12500,
            )
    assert result["status"] == "pushed"
    assert result["telegram_message_id"] == 100
    assert result["thread_message_id"] == 200
    assert result["body_message_id"] == 201
    assert result["link_message_id"] == 202
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


def test_wait_for_auto_forward_strict_match_under_race():
    """Regression: when getUpdates returns auto-forwards from MULTIPLE channel msgs
    (parallel publishers race), this publisher must match ONLY its own channel_msg_id.

    Pre-fix bug: `is_auto OR fwd_msg == X` short-circuited via is_auto=True →
    matched FIRST forward (50) instead of own (100), causing replies to land in
    the wrong thread. Fix: require fwd_msg == channel_msg_id strictly.
    """
    p = TelegramPublisher("t", "c", "http://x", linked_group_chat_id="g-1")
    responses = [
        # drain
        {"ok": True, "result": []},
        # channel post succeeds → msg 100
        {"ok": True, "result": {"message_id": 100}},
        # poll returns 3 auto-forwards: 50 (someone else's), 100 (ours), 200 (someone else's)
        {"ok": True, "result": [
            {"update_id": 1, "message": {
                "message_id": 500, "chat": {"id": "g-1"},
                "is_automatic_forward": True, "forward_from_message_id": 50,
            }},
            {"update_id": 2, "message": {
                "message_id": 501, "chat": {"id": "g-1"},
                "is_automatic_forward": True, "forward_from_message_id": 100,
            }},
            {"update_id": 3, "message": {
                "message_id": 502, "chat": {"id": "g-1"},
                "is_automatic_forward": True, "forward_from_message_id": 200,
            }},
        ]},
        # thread reply 1 — body
        {"ok": True, "result": {"message_id": 600}},
        # thread reply 2 — link
        {"ok": True, "result": {"message_id": 601}},
    ]
    with patch("lib.telegram_publisher.time.sleep"):
        with patch("lib.telegram_publisher.urllib.request.urlopen",
                   side_effect=_mock_urlopen_factory(responses)):
            result = p.publish_article_with_thread_body("T", "B", "s")
    assert result["status"] == "pushed"
    assert result["telegram_message_id"] == 100
    # Must pick 501 (forward of 100) — NOT 500 (forward of 50, the first in poll)
    assert result["thread_message_id"] == 501
    assert result["body_message_id"] == 600
    assert result["link_message_id"] == 601


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


# ===== T14b — duration + tokens formatters =====


def test_format_duration_seconds_only():
    assert _format_duration(45000) == "45s"
    assert _format_duration(1000) == "1s"


def test_format_duration_minutes_and_seconds():
    assert _format_duration(204000) == "3m 24s"
    assert _format_duration(60000) == "1m 0s"
    assert _format_duration(3661000) == "61m 1s"


def test_format_duration_none_or_zero_returns_none():
    """Phase G T16: None/0 → None (caller skips field, không hiện '—')."""
    assert _format_duration(None) is None
    assert _format_duration(0) is None
    assert _format_duration(-5) is None


def test_format_tokens_with_separator():
    assert _format_tokens(12500) == "12.500"
    assert _format_tokens(1234567) == "1.234.567"
    assert _format_tokens(100) == "100"


def test_format_tokens_none_returns_none():
    """Phase G T16: None/0 → None (caller skips, không hiện '—')."""
    assert _format_tokens(None) is None
    assert _format_tokens(0) is None


# ===== T16 — _build_channel_text 4 cases (both / duration only / tokens only / neither) =====

VN_TZ_TEST = timezone(timedelta(hours=7))
FIXED_TIME = datetime(2026, 5, 10, 22, 30, 45, tzinfo=VN_TZ_TEST)
ESCAPE_NOOP = lambda s: s  # tests use plain titles, no escape needed


def test_build_channel_text_both_duration_and_tokens():
    text = _build_channel_text("Title", FIXED_TIME, 204000, 12500, ESCAPE_NOOP)
    assert text == (
        "<b>Title</b>\n"
        "\n"  # blank line cho thoáng
        "🕐 10/05/2026 22:30:45\n"
        "⏱️ Thời gian viết bài: 3m 24s · 🪙 12.500"
    )


def test_build_channel_text_duration_only_tokens_none():
    text = _build_channel_text("Title", FIXED_TIME, 97000, None, ESCAPE_NOOP)
    assert text == (
        "<b>Title</b>\n"
        "\n"
        "🕐 10/05/2026 22:30:45\n"
        "⏱️ Thời gian viết bài: 1m 37s"
    )


def test_build_channel_text_tokens_only_duration_none():
    """Duration null → fallback 'chưa đo'; tokens present → joined với ' · '."""
    text = _build_channel_text("Title", FIXED_TIME, None, 8500, ESCAPE_NOOP)
    assert text == (
        "<b>Title</b>\n"
        "\n"
        "🕐 10/05/2026 22:30:45\n"
        "⏱️ Thời gian viết bài: chưa đo · 🪙 8.500"
    )


def test_build_channel_text_both_none_uses_fallback():
    """Line 3 ALWAYS present for visual consistency — duration falls back to 'chưa đo'."""
    text = _build_channel_text("Title", FIXED_TIME, None, 0, ESCAPE_NOOP)
    assert text == (
        "<b>Title</b>\n"
        "\n"
        "🕐 10/05/2026 22:30:45\n"
        "⏱️ Thời gian viết bài: chưa đo"
    )
    assert "⏱️" in text  # line 3 emitted
    assert "🪙" not in text  # tokens absent → no token chunk
    assert "—" not in text  # no em dash placeholder


def test_build_channel_text_escapes_title():
    """HTML escape title containing < > &."""
    text = _build_channel_text("A & B <bad>", FIXED_TIME, None, None,
                               lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    assert "<b>A &amp; B &lt;bad&gt;</b>" in text


# === V5.1.8 publish_article_v5 — Gemini+Grok only, no Claude push ===========


from lib.telegram_publisher import _build_channel_text_v5, _format_cost  # noqa: E402


def test_format_cost_renders_dollar_4_decimals():
    assert _format_cost(0.0247) == "$0.0247"
    assert _format_cost(1.2345) == "$1.2345"
    assert _format_cost(None) is None
    assert _format_cost(0) is None
    assert _format_cost(-0.01) is None


def test_build_channel_text_v5_both_titles():
    text = _build_channel_text_v5(
        gemini_title="Chủ tịch VHM vạch ranh giới: ai sống?",
        grok_title="VHM chọn lọc 2026: tiêu chí loại ai",
        posted_at=FIXED_TIME,
        duration_ms=97000,
        cost_usd=0.0247,
        escape_fn=ESCAPE_NOOP,
    )
    assert "<b>Gemini:</b> Chủ tịch VHM vạch ranh giới: ai sống?" in text
    assert "<b>grok:</b> VHM chọn lọc 2026: tiêu chí loại ai" in text
    assert "💰 $0.0247" in text
    assert "⏱️ Viết: 1m 37s" in text


def test_build_channel_text_v5_gemini_only():
    """Only Gemini side present → single title line."""
    text = _build_channel_text_v5(
        gemini_title="G title",
        grok_title=None,
        posted_at=FIXED_TIME,
        duration_ms=None,
        cost_usd=None,
        escape_fn=ESCAPE_NOOP,
    )
    assert "<b>Gemini:</b> G title" in text
    assert "<b>grok:</b>" not in text


def test_publish_v5_skipped_when_both_titles_missing():
    p = TelegramPublisher("t", "c", "http://x", linked_group_chat_id="g-1")
    result = p.publish_article_v5(
        gemini_title=None,
        grok_title=None,
        gemini_body=None,
        grok_body=None,
        public_slug="slug",
    )
    assert result["status"] == "skipped_no_parallel_writers"
    assert result["telegram_message_id"] is None
    assert "no parallel writers succeeded" in result["error"]


def test_publish_v5_no_linked_group_falls_back_to_legacy_single():
    """Without linked_group_chat_id, V5 method posts a single legacy-style
    channel message using whichever title is available."""
    p = TelegramPublisher("t", "c", "http://x")  # linked_group_chat_id=None
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({
        "ok": True, "result": {"message_id": 99},
    }).encode("utf-8")
    mock_resp.__enter__ = lambda self: self
    mock_resp.__exit__ = lambda *args: None

    with patch("lib.telegram_publisher.urllib.request.urlopen", return_value=mock_resp):
        result = p.publish_article_v5(
            gemini_title="G",
            grok_title=None,
            gemini_body="body G",
            grok_body=None,
            public_slug="vhm-slug",
        )
    assert result["status"] == "pushed"
    assert result["telegram_message_id"] == 99
    # Legacy fallback fields added
    assert result["thread_message_id"] is None
    assert result["gemini_body_message_id"] is None
    assert result["grok_body_message_id"] is None
