"""Telegram Bot API publisher (Phase G T12 + T14b).

Two-stage publish:
1. Channel post: title bold ONLY (clean broadcast feed)
2. Auto-forward to linked discussion group (Telegram does this automatically
   when channel + group are linked)
3. Bot detects auto-forward via getUpdates polling
4. Bot replies in that thread with full Master body — readers click
   "Leave a comment" on channel post → opens thread → see full article + can comment

Bot must be admin in BOTH:
- Channel (with Post Messages permission)
- Linked discussion group (privacy mode auto-disabled cho admins → bot sees auto-forwards)

Idempotent via generated_news.telegram_pushed_at (Phase G T11 schema column).
Graceful degrade when secrets.yaml missing (returns None publisher).
"""
from __future__ import annotations
import json
import re
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml

VN_TZ = timezone(timedelta(hours=7))


def _format_duration(ms: int | None) -> str:
    """Format duration_ms → human-readable. None/0 → '—' placeholder."""
    if ms is None or ms <= 0:
        return "—"
    seconds = ms // 1000
    if seconds < 60:
        return f"{seconds}s"
    minutes, sec = divmod(seconds, 60)
    return f"{minutes}m {sec}s"


def _format_tokens(n: int | None) -> str:
    """Format token count với separator. None → '—' placeholder."""
    if n is None or n <= 0:
        return "—"
    return f"{n:,}".replace(",", ".")  # Vietnamese number separator


def _md_to_telegram_html(body: str) -> str:
    """Convert Master Markdown body → Telegram HTML parse_mode subset.

    Telegram HTML supports: <b>, <i>, <u>, <s>, <a>, <code>, <pre>, <blockquote>.
    Does NOT support: <ul>/<li>, <h1>/<h2>, <p>. Newlines preserved.

    Conversions:
    - `- text` (bullet list) → `• text`
    - `**bold**` → `<b>bold</b>`
    - `## Heading` / `### Heading` → `<b>Heading</b>`
    """
    out = body
    # Bullets: line starting with `- ` → `• `
    out = re.sub(r'^- ', '• ', out, flags=re.MULTILINE)
    # Bold: **text** → <b>text</b>
    out = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', out)
    # Headings (h2/h3) → <b>...</b>
    out = re.sub(r'^#{2,3}\s+(.+)$', r'<b>\1</b>', out, flags=re.MULTILINE)
    return out


class TelegramPublisher:
    """Two-stage publisher: channel title + thread body in linked group."""

    def __init__(
        self,
        bot_token: str,
        chat_id: str,
        base_url: str,
        linked_group_chat_id: str | None = None,
    ) -> None:
        self.bot_token = bot_token
        self.chat_id = chat_id  # channel chat_id
        self.base_url = base_url.rstrip("/")
        self.linked_group_chat_id = linked_group_chat_id  # optional — None disables thread reply

    def _api(self, method: str, data: dict, timeout: int = 10) -> dict:
        """POST to Bot API. Returns parsed JSON; on exception returns {ok: false, description: str(e)}."""
        url = f"https://api.telegram.org/bot{self.bot_token}/{method}"
        encoded = urllib.parse.urlencode(data).encode("utf-8")
        try:
            with urllib.request.urlopen(url, data=encoded, timeout=timeout) as resp:
                return json.loads(resp.read())
        except Exception as e:
            return {"ok": False, "description": str(e)}

    def publish_article(self, title: str, public_slug: str) -> dict:
        """LEGACY (T12) — push title + URL to channel as single message.

        Used when linked_group_chat_id is None or thread-reply not desired.
        Returns {status, telegram_message_id, error}.
        """
        message = f"<b>{self._escape_html(title)}</b>\n\n{self.base_url}/article/{public_slug}"
        result = self._api("sendMessage", {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": "false",
        })
        if result.get("ok"):
            return {
                "status": "pushed",
                "telegram_message_id": result["result"]["message_id"],
                "error": None,
            }
        return {
            "status": "failed",
            "telegram_message_id": None,
            "error": result.get("description", "Telegram API returned ok=False"),
        }

    def publish_article_with_thread_body(
        self,
        title: str,
        body: str,
        public_slug: str,
        posted_at: datetime | None = None,
        write_duration_ms: int | None = None,
        tokens: int | None = None,
        max_poll_attempts: int = 8,
        poll_interval_sec: float = 2.0,
    ) -> dict:
        """T14b — Two-stage publish (channel 3 lines + 2 thread messages):

        Channel post (3 lines):
            Line 1: <b>{title}</b>
            Line 2: 🕐 {posted_at:%d/%m/%Y %H:%M:%S}
            Line 3: ⏱️ {duration} · 🪙 {tokens}

        Thread message 1: full Master body (Markdown→HTML converted)
        Thread message 2: link to web detail (📚 Xem đầy đủ phản biện + nguồn + pipeline log)

        Args:
            posted_at: timestamp for line 2 — defaults to datetime.now(VN_TZ)
            write_duration_ms: total Master + Skeptic duration → line 3 ⏱️
            tokens: total Master + Skeptic tokens → line 3 🪙 (use '—' if None)

        Returns {status, telegram_message_id, thread_message_id, body_message_id, link_message_id, error}.
        """
        if self.linked_group_chat_id is None:
            return self.publish_article(title, public_slug)

        if posted_at is None:
            posted_at = datetime.now(VN_TZ)

        # Step 0: drain stale getUpdates
        offset = self._drain_offset()

        # Step 1: post 3-line channel message
        channel_text = (
            f"<b>{self._escape_html(title)}</b>\n"
            f"🕐 {posted_at.strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"⏱️ {_format_duration(write_duration_ms)} · 🪙 {_format_tokens(tokens)}"
        )
        ch_result = self._api("sendMessage", {
            "chat_id": self.chat_id,
            "text": channel_text,
            "parse_mode": "HTML",
        })
        if not ch_result.get("ok"):
            return {
                "status": "failed",
                "telegram_message_id": None,
                "error": ch_result.get("description", "Channel post failed"),
                "thread_message_id": None,
                "body_message_id": None,
                "link_message_id": None,
            }
        ch_msg_id = ch_result["result"]["message_id"]

        # Step 2: poll for auto-forward in linked group
        thread_msg_id = self._wait_for_auto_forward(
            channel_msg_id=ch_msg_id,
            offset=offset,
            max_attempts=max_poll_attempts,
            interval_sec=poll_interval_sec,
        )

        if thread_msg_id is None:
            return {
                "status": "pushed_no_thread",
                "telegram_message_id": ch_msg_id,
                "error": "auto-forward not detected within poll window — thread replies skipped",
                "thread_message_id": None,
                "body_message_id": None,
                "link_message_id": None,
            }

        # Step 3a: thread reply 1 — full Master body
        body_html = _md_to_telegram_html(body)
        body_result = self._api("sendMessage", {
            "chat_id": self.linked_group_chat_id,
            "text": body_html,
            "parse_mode": "HTML",
            "reply_to_message_id": thread_msg_id,
        })
        if not body_result.get("ok"):
            return {
                "status": "pushed_no_thread",
                "telegram_message_id": ch_msg_id,
                "error": f"thread body reply failed: {body_result.get('description')}",
                "thread_message_id": thread_msg_id,
                "body_message_id": None,
                "link_message_id": None,
            }
        body_msg_id = body_result["result"]["message_id"]

        # Step 3b: thread reply 2 — link to web detail
        # Telegram parse_mode=HTML không auto-linkify plain URL → wrap explicit <a href>
        article_url = f"{self.base_url}/article/{public_slug}"
        link_text = (
            "📚 Đọc đầy đủ <b>phản biện</b>, <b>nguồn tra cứu</b>, <b>pipeline log</b>:\n"
            f'<a href="{article_url}">{article_url}</a>'
        )
        link_result = self._api("sendMessage", {
            "chat_id": self.linked_group_chat_id,
            "text": link_text,
            "parse_mode": "HTML",
            "reply_to_message_id": thread_msg_id,
            "disable_web_page_preview": "false",
        })
        link_msg_id = link_result["result"]["message_id"] if link_result.get("ok") else None

        return {
            "status": "pushed",
            "telegram_message_id": ch_msg_id,
            "error": None if link_msg_id else f"link reply failed: {link_result.get('description')}",
            "thread_message_id": thread_msg_id,
            "body_message_id": body_msg_id,
            "link_message_id": link_msg_id,
        }

    def _drain_offset(self) -> int:
        """Consume any stale getUpdates so subsequent polls see only fresh events.
        Returns offset for next poll (max_seen_update_id + 1).
        """
        result = self._api("getUpdates", {"limit": 100, "timeout": 0})
        if not result.get("ok") or not result.get("result"):
            return 0
        max_uid = max(u["update_id"] for u in result["result"])
        # Acknowledge consumed
        self._api("getUpdates", {"offset": max_uid + 1, "limit": 1, "timeout": 0})
        return max_uid + 1

    def _wait_for_auto_forward(
        self,
        channel_msg_id: int,
        offset: int,
        max_attempts: int,
        interval_sec: float,
    ) -> int | None:
        """Poll getUpdates; return msg_id of auto-forwarded post in linked group.

        Match criteria:
        - chat.id == self.linked_group_chat_id
        - is_automatic_forward == True OR forward_from_message_id == channel_msg_id
        """
        current_offset = offset
        for _ in range(max_attempts):
            time.sleep(interval_sec)
            upd = self._api("getUpdates", {"offset": current_offset, "limit": 100, "timeout": 1})
            if not upd.get("ok"):
                continue
            for u in upd.get("result", []):
                current_offset = max(current_offset, u["update_id"] + 1)
                msg = u.get("message") or {}
                chat_id = str(msg.get("chat", {}).get("id", ""))
                if chat_id != str(self.linked_group_chat_id):
                    continue
                is_auto = msg.get("is_automatic_forward", False)
                fwd_msg = msg.get("forward_from_message_id")
                if is_auto or fwd_msg == channel_msg_id:
                    return msg["message_id"]
        return None

    @staticmethod
    def _escape_html(text: str) -> str:
        """Escape & < > for Telegram parse_mode=HTML — order matters (& first)."""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def load_telegram_config(secrets_path: Path = Path("data/secrets.yaml")) -> TelegramPublisher | None:
    """Load TG config from secrets.yaml. Returns None if file missing or section incomplete.

    Required keys: telegram.{bot_token, chat_id, base_url}
    Optional: telegram.linked_group_chat_id (enables thread reply per T14b)
    Graceful: caller treats None as 'Telegram disabled' and skips push.
    """
    if not secrets_path.exists():
        return None
    config = yaml.safe_load(secrets_path.read_text(encoding="utf-8"))
    tg = config.get("telegram") if config else None
    if not tg or not all(k in tg for k in ("bot_token", "chat_id", "base_url")):
        return None
    return TelegramPublisher(
        bot_token=tg["bot_token"],
        chat_id=tg["chat_id"],
        base_url=tg["base_url"],
        linked_group_chat_id=tg.get("linked_group_chat_id"),  # optional
    )
