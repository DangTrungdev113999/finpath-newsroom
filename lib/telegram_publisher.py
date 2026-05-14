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
import fcntl
import json
import re
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml

VN_TZ = timezone(timedelta(hours=7))

# Cross-process advisory lock — serializes ALL publishers sharing the same bot.
# Telegram getUpdates queue is destructive (acked updates vanish for other readers),
# so parallel publishers race on auto-forward detection. fcntl.flock guards the
# entire post+poll sequence per channel.
_LOCK_PATH = Path("/tmp/finpath-newsroom-tg-publisher.lock")


def _format_duration(ms: int | None) -> str | None:
    """Format duration_ms → human-readable. None/0 → None (caller skips field)."""
    if ms is None or ms <= 0:
        return None
    seconds = ms // 1000
    if seconds < 60:
        return f"{seconds}s"
    minutes, sec = divmod(seconds, 60)
    return f"{minutes}m {sec}s"


def _format_tokens(n: int | None) -> str | None:
    """Format token count với Vietnamese separator. None/0 → None."""
    if n is None or n <= 0:
        return None
    return f"{n:,}".replace(",", ".")


def _format_cost(cost_usd: float | None) -> str | None:
    """Format USD cost → '$0.0247'. None/0 → None (caller skips field)."""
    if cost_usd is None or cost_usd <= 0:
        return None
    return f"${cost_usd:.4f}"


def _build_channel_text_v5(
    *,
    gemini_title: str | None,
    grok_title: str | None,
    posted_at: datetime,
    duration_ms: int | None,
    cost_usd: float | None,
    escape_fn,
) -> str:
    """V5.1.8 channel post — 1 line per available parallel writer + meta.

    Format:
        <b>Gemini:</b> {gemini_title}    # only if gemini_title present
        <b>grok:</b> {grok_title}        # only if grok_title present
        [blank line]
        🕐 {posted_at}
        ⏱️ Viết: {duration} · 💰 {cost}

    At least one of gemini_title / grok_title MUST be present — caller
    enforces this via 'skipped_no_parallel_writers' branch.
    """
    title_lines: list[str] = []
    if gemini_title:
        title_lines.append(f"<b>Gemini:</b> {escape_fn(gemini_title)}")
    if grok_title:
        title_lines.append(f"<b>grok:</b> {escape_fn(grok_title)}")

    duration_str = _format_duration(duration_ms) or "chưa đo"
    cost_str = _format_cost(cost_usd)
    meta_parts = [f"⏱️ Viết: {duration_str}"]
    if cost_str:
        meta_parts.append(f"💰 {cost_str}")

    lines = [
        *title_lines,
        "",
        f"🕐 {posted_at.strftime('%d/%m/%Y %H:%M:%S')}",
        " · ".join(meta_parts),
    ]
    return "\n".join(lines)


def _build_channel_text(title: str, posted_at: datetime, duration_ms: int | None,
                       tokens: int | None, escape_fn) -> str:
    """Build channel post — always 3 lines for visual consistency.

    Format:
        <b>{title}</b>
        [blank line]
        🕐 {posted_at}
        ⏱️ Thời gian viết bài: {duration|chưa đo}[ · 🪙 {tokens}]

    Line 3 ALWAYS present — duration falls back to "chưa đo" when null
    so feed renders consistently regardless of upstream timing logs.
    """
    duration_str = _format_duration(duration_ms) or "chưa đo"
    tokens_str = _format_tokens(tokens)

    parts = [f"⏱️ Thời gian viết bài: {duration_str}"]
    if tokens_str:
        parts.append(f"🪙 {tokens_str}")

    lines = [
        f"<b>{escape_fn(title)}</b>",
        "",
        f"🕐 {posted_at.strftime('%d/%m/%Y %H:%M:%S')}",
        " · ".join(parts),
    ]
    return "\n".join(lines)


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

        # Serialize via cross-process advisory lock — parallel publishers sharing
        # the same bot race on getUpdates queue (destructive ack). Lock spans
        # drain + send + poll so each post's auto-forward is detected cleanly.
        with _LOCK_PATH.open("a") as lockfile:
            fcntl.flock(lockfile.fileno(), fcntl.LOCK_EX)
            try:
                return self._publish_locked(
                    title=title,
                    body=body,
                    public_slug=public_slug,
                    posted_at=posted_at,
                    write_duration_ms=write_duration_ms,
                    tokens=tokens,
                    max_poll_attempts=max_poll_attempts,
                    poll_interval_sec=poll_interval_sec,
                )
            finally:
                fcntl.flock(lockfile.fileno(), fcntl.LOCK_UN)

    def _publish_locked(
        self,
        title: str,
        body: str,
        public_slug: str,
        posted_at: datetime,
        write_duration_ms: int | None,
        tokens: int | None,
        max_poll_attempts: int,
        poll_interval_sec: float,
    ) -> dict:
        """Internal — runs inside cross-process lock acquired by caller."""
        # Step 0: drain stale getUpdates
        offset = self._drain_offset()

        # Step 1: post channel message với conditional line 3 (skip nếu cả 2 None)
        channel_text = _build_channel_text(
            title=title,
            posted_at=posted_at,
            duration_ms=write_duration_ms,
            tokens=tokens,
            escape_fn=self._escape_html,
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

    def publish_article_v5(
        self,
        *,
        gemini_title: str | None,
        grok_title: str | None,
        gemini_body: str | None,
        grok_body: str | None,
        public_slug: str,
        posted_at: datetime | None = None,
        total_duration_ms: int | None = None,
        total_cost_usd: float | None = None,
        max_poll_attempts: int = 8,
        poll_interval_sec: float = 2.0,
    ) -> dict:
        """V5.1.8 — Push parallel-writer titles only (Claude side excluded).

        Channel post lines (1 per available side):
            <b>Gemini:</b> {gemini_title}
            <b>grok:</b> {grok_title}

        Thread replies (3 messages):
            1. <b>📰 Bài Gemini</b> + body (skipped if gemini_body missing)
            2. <b>📰 Bài Grok</b> + body (skipped if grok_body missing)
            3. CTA: 📚 Đọc đầy đủ + nguồn + comments: {url}

        Skip rules:
            - Both titles missing → status='skipped_no_parallel_writers'
              (no API call, no telegram_pushed_at set; orchestrator may retry
              next pipeline run if Gemini/Grok succeed later).
            - Only one title present → 1-line channel post + 1 body reply + CTA.
            - linked_group_chat_id is None → fall back to legacy publish_article
              with the available title (no thread).

        Returns same shape as publish_article_with_thread_body plus
        'gemini_body_message_id' + 'grok_body_message_id' (both nullable).
        """
        if not gemini_title and not grok_title:
            return {
                "status": "skipped_no_parallel_writers",
                "telegram_message_id": None,
                "thread_message_id": None,
                "gemini_body_message_id": None,
                "grok_body_message_id": None,
                "link_message_id": None,
                "error": "both gemini_title and grok_title missing — no parallel writers succeeded",
            }

        if self.linked_group_chat_id is None:
            # No linked discussion group → degrade to single channel message
            # with the better-available title.
            fallback_title = gemini_title or grok_title or ""
            legacy = self.publish_article(fallback_title, public_slug)
            legacy["thread_message_id"] = None
            legacy["gemini_body_message_id"] = None
            legacy["grok_body_message_id"] = None
            legacy["link_message_id"] = None
            return legacy

        if posted_at is None:
            posted_at = datetime.now(VN_TZ)

        with _LOCK_PATH.open("a") as lockfile:
            fcntl.flock(lockfile.fileno(), fcntl.LOCK_EX)
            try:
                return self._publish_v5_locked(
                    gemini_title=gemini_title,
                    grok_title=grok_title,
                    gemini_body=gemini_body,
                    grok_body=grok_body,
                    public_slug=public_slug,
                    posted_at=posted_at,
                    total_duration_ms=total_duration_ms,
                    total_cost_usd=total_cost_usd,
                    max_poll_attempts=max_poll_attempts,
                    poll_interval_sec=poll_interval_sec,
                )
            finally:
                fcntl.flock(lockfile.fileno(), fcntl.LOCK_UN)

    def _publish_v5_locked(
        self,
        *,
        gemini_title: str | None,
        grok_title: str | None,
        gemini_body: str | None,
        grok_body: str | None,
        public_slug: str,
        posted_at: datetime,
        total_duration_ms: int | None,
        total_cost_usd: float | None,
        max_poll_attempts: int,
        poll_interval_sec: float,
    ) -> dict:
        offset = self._drain_offset()
        channel_text = _build_channel_text_v5(
            gemini_title=gemini_title,
            grok_title=grok_title,
            posted_at=posted_at,
            duration_ms=total_duration_ms,
            cost_usd=total_cost_usd,
            escape_fn=self._escape_html,
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
                "thread_message_id": None,
                "gemini_body_message_id": None,
                "grok_body_message_id": None,
                "link_message_id": None,
                "error": ch_result.get("description", "Channel post failed"),
            }
        ch_msg_id = ch_result["result"]["message_id"]

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
                "thread_message_id": None,
                "gemini_body_message_id": None,
                "grok_body_message_id": None,
                "link_message_id": None,
                "error": "auto-forward not detected within poll window — thread replies skipped",
            }

        # Reply 1 — Gemini body (skip if not provided)
        gemini_body_msg_id: int | None = None
        if gemini_body:
            text = "<b>📰 Bài Gemini</b>\n\n" + _md_to_telegram_html(gemini_body)
            r = self._api("sendMessage", {
                "chat_id": self.linked_group_chat_id,
                "text": text,
                "parse_mode": "HTML",
                "reply_to_message_id": thread_msg_id,
            })
            if r.get("ok"):
                gemini_body_msg_id = r["result"]["message_id"]

        # Reply 2 — Grok body (skip if not provided)
        grok_body_msg_id: int | None = None
        if grok_body:
            text = "<b>📰 Bài Grok</b>\n\n" + _md_to_telegram_html(grok_body)
            r = self._api("sendMessage", {
                "chat_id": self.linked_group_chat_id,
                "text": text,
                "parse_mode": "HTML",
                "reply_to_message_id": thread_msg_id,
            })
            if r.get("ok"):
                grok_body_msg_id = r["result"]["message_id"]

        # Reply 3 — CTA web link (always sent)
        article_url = f"{self.base_url}/article/{public_slug}"
        link_text = (
            "📚 Đọc đầy đủ <b>3 bản</b> (Claude / Gemini / Grok), <b>ảnh hero</b>, "
            "<b>nguồn tra cứu</b>, <b>pipeline log</b>:\n"
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
            "thread_message_id": thread_msg_id,
            "gemini_body_message_id": gemini_body_msg_id,
            "grok_body_message_id": grok_body_msg_id,
            "link_message_id": link_msg_id,
            "error": None,
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

        Match criteria (STRICT — fwd_msg must equal this channel_msg_id):
        - chat.id == self.linked_group_chat_id
        - forward_from_message_id == channel_msg_id

        Why strict: the previous `is_automatic_forward OR fwd_msg == X` raced when
        parallel publishers shared the bot — `is_auto=True` short-circuited to the
        FIRST forward in the poll window regardless of which channel msg spawned it.
        Requiring fwd_msg equality makes detection deterministic per-post even under
        concurrency. is_automatic_forward is still implied (only auto-forwards from
        linked channel carry the same forward_from_message_id semantics).
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
                if msg.get("forward_from_message_id") == channel_msg_id:
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
