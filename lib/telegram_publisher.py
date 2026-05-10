"""Telegram Bot API publisher (Phase G T12).

After Skeptic completes critique, push title + article URL to Telegram group.
Idempotent via generated_news.telegram_pushed_at (Phase G T11 schema column).
Graceful degrade when secrets.yaml missing (returns None publisher).
"""
from __future__ import annotations
import json
import urllib.request
import urllib.parse
from pathlib import Path

import yaml


class TelegramPublisher:
    """Send notification to Telegram via Bot API sendMessage endpoint."""

    def __init__(self, bot_token: str, chat_id: str, base_url: str) -> None:
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = base_url.rstrip("/")

    def publish_article(self, title: str, public_slug: str) -> dict:
        """Push notification. Returns {status, telegram_message_id, error}.

        status values:
        - "pushed" — Telegram returned ok=True
        - "failed" — network error OR Telegram returned ok=False
        """
        message = f"<b>{self._escape_html(title)}</b>\n\n{self.base_url}/article/{public_slug}"
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": "false",
        }).encode("utf-8")
        try:
            with urllib.request.urlopen(url, data=data, timeout=10) as resp:
                result = json.loads(resp.read())
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
        except Exception as e:
            return {
                "status": "failed",
                "telegram_message_id": None,
                "error": str(e),
            }

    @staticmethod
    def _escape_html(text: str) -> str:
        """Escape & < > for Telegram parse_mode=HTML — order matters (& first)."""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def load_telegram_config(secrets_path: Path = Path("data/secrets.yaml")) -> TelegramPublisher | None:
    """Load TG config from secrets.yaml. Returns None if file missing or section incomplete.

    Required keys: telegram.{bot_token, chat_id, base_url}.
    Graceful: caller treats None as 'Telegram disabled' and skips push.
    """
    if not secrets_path.exists():
        return None
    config = yaml.safe_load(secrets_path.read_text(encoding="utf-8"))
    tg = config.get("telegram") if config else None
    if not tg or not all(k in tg for k in ("bot_token", "chat_id", "base_url")):
        return None
    return TelegramPublisher(tg["bot_token"], tg["chat_id"], tg["base_url"])
