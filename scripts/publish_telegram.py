#!/usr/bin/env python3
"""Telegram publisher CLI — T14b idempotent publish."""
import sys
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.telegram_publisher import load_telegram_config

VN_TZ = timezone(timedelta(hours=7))


def publish_article_telegram(
    article_id: str,
    channel_footer_warning: str | None = None,
) -> dict:
    """Publish article to Telegram với T14b idempotency check.

    Args:
        article_id: UUID from generated_news.article_id
        channel_footer_warning: Optional warning to append to link message

    Returns:
        {status, message, telegram_message_id, thread_message_id, error}
    """
    # Load config
    publisher = load_telegram_config()
    if publisher is None:
        return {
            "status": "skipped",
            "message": "secrets.yaml missing or incomplete — Telegram disabled",
            "error": None,
        }

    # Connect DB
    db_path = Path(__file__).parent.parent / "data" / "pipeline.db"
    if not db_path.exists():
        return {
            "status": "failed",
            "message": f"Database not found: {db_path}",
            "error": "DB_NOT_FOUND",
        }

    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()

    # Check idempotency
    c.execute(
        "SELECT telegram_pushed_at FROM generated_news WHERE article_id = ?",
        (article_id,),
    )
    row = c.fetchone()
    if row is None:
        conn.close()
        return {
            "status": "failed",
            "message": f"Article {article_id} not found in DB",
            "error": "ARTICLE_NOT_FOUND",
        }

    if row[0] is not None:
        conn.close()
        return {
            "status": "skipped",
            "message": f"Already pushed at {row[0]} — idempotency check passed",
            "error": None,
        }

    # Load article data
    c.execute(
        """
        SELECT title, body, public_slug, published_at, pipeline_log
        FROM generated_news
        WHERE article_id = ?
        """,
        (article_id,),
    )
    row = c.fetchone()
    title, body, public_slug, published_at_str, pipeline_log = row

    # Parse posted_at
    if published_at_str:
        posted_at = datetime.fromisoformat(published_at_str)
    else:
        posted_at = datetime.now(VN_TZ)

    # Extract duration + tokens from pipeline_log (if available)
    # Format expected: JSON with master_duration_ms, skeptic_duration_ms, master_tokens, skeptic_tokens
    write_duration_ms = None
    tokens = None
    if pipeline_log:
        import json
        try:
            log_data = json.loads(pipeline_log)
            master_dur = log_data.get("master_duration_ms") or 0
            skeptic_dur = log_data.get("skeptic_duration_ms") or 0
            write_duration_ms = master_dur + skeptic_dur if master_dur or skeptic_dur else None

            master_tok = log_data.get("master_tokens") or 0
            skeptic_tok = log_data.get("skeptic_tokens") or 0
            tokens = master_tok + skeptic_tok if master_tok or skeptic_tok else None
        except (json.JSONDecodeError, KeyError):
            pass  # gracefully degrade

    # Append warning to body if provided
    if channel_footer_warning:
        body = f"{body}\n\n⚠️ {channel_footer_warning}"

    # Publish
    result = publisher.publish_article_with_thread_body(
        title=title,
        body=body,
        public_slug=public_slug,
        posted_at=posted_at,
        write_duration_ms=write_duration_ms,
        tokens=tokens,
    )

    # Update DB if success
    if result["status"] in ("pushed", "pushed_no_thread"):
        now_utc = datetime.now(timezone.utc).isoformat()
        c.execute(
            "UPDATE generated_news SET telegram_pushed_at = ? WHERE article_id = ?",
            (now_utc, article_id),
        )
        conn.commit()

    conn.close()

    return {
        "status": result["status"],
        "message": f"Telegram publish: {result['status']}",
        "telegram_message_id": result.get("telegram_message_id"),
        "thread_message_id": result.get("thread_message_id"),
        "body_message_id": result.get("body_message_id"),
        "link_message_id": result.get("link_message_id"),
        "error": result.get("error"),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/publish_telegram.py <article_id> [channel_footer_warning]")
        sys.exit(1)

    article_id = sys.argv[1]
    warning = sys.argv[2] if len(sys.argv) > 2 else None

    result = publish_article_telegram(article_id, warning)

    print(f"\n{'='*60}")
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    if result.get("telegram_message_id"):
        print(f"Channel message ID: {result['telegram_message_id']}")
    if result.get("thread_message_id"):
        print(f"Thread message ID: {result['thread_message_id']}")
    if result.get("body_message_id"):
        print(f"Body message ID: {result['body_message_id']}")
    if result.get("link_message_id"):
        print(f"Link message ID: {result['link_message_id']}")
    if result.get("error"):
        print(f"⚠️  Error: {result['error']}")
    print(f"{'='*60}\n")

    sys.exit(0 if result["status"] in ("pushed", "pushed_no_thread", "skipped") else 1)
