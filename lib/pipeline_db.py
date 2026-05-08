"""SQLite ops cho pipeline state — crawl_log + generated_news."""
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Any


class PipelineDB:
    """SQLite handle for crawl_log + generated_news."""

    def __init__(self, path: str | Path) -> None:
        self.path = str(path)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")

    def init_schema(self, schema_path: str | Path) -> None:
        sql = Path(schema_path).read_text(encoding="utf-8")
        self.conn.executescript(sql)
        self.conn.commit()

    def list_tables(self) -> list[str]:
        cur = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        return [r["name"] for r in cur.fetchall()]

    def insert_crawl_row(self, data: dict[str, Any]) -> str:
        cols = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        sql = f"INSERT INTO crawl_log ({cols}) VALUES ({placeholders})"
        self.conn.execute(sql, list(data.values()))
        self.conn.commit()
        return data["row_id"]

    def get_crawl_row(self, row_id: str) -> dict[str, Any] | None:
        cur = self.conn.execute("SELECT * FROM crawl_log WHERE row_id = ?", (row_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def update_crawl_row(self, row_id: str, updates: dict[str, Any]) -> None:
        if not updates:
            return
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        sql = f"UPDATE crawl_log SET {set_clause} WHERE row_id = ?"
        self.conn.execute(sql, [*updates.values(), row_id])
        self.conn.commit()

    def query_by_funnel_batch(self, batch_id: str) -> list[dict[str, Any]]:
        cur = self.conn.execute(
            "SELECT * FROM crawl_log WHERE funnel_batch_id = ? ORDER BY crawled_at DESC",
            (batch_id,),
        )
        return [dict(r) for r in cur.fetchall()]

    def query_pending_for_editor(self) -> list[dict[str, Any]]:
        cur = self.conn.execute(
            "SELECT * FROM crawl_log WHERE status = 'pending' AND editor_v1_decision IS NULL"
        )
        return [dict(r) for r in cur.fetchall()]

    def insert_generated_news(self, data: dict[str, Any]) -> str:
        cols = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        sql = f"INSERT INTO generated_news ({cols}) VALUES ({placeholders})"
        self.conn.execute(sql, list(data.values()))
        self.conn.commit()
        return data["article_id"]

    def update_generated_news(self, article_id: str, updates: dict[str, Any]) -> None:
        if not updates:
            return
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        sql = f"UPDATE generated_news SET {set_clause} WHERE article_id = ?"
        self.conn.execute(sql, [*updates.values(), article_id])
        self.conn.commit()

    def recent_generated_news(self, ticker: str, limit: int = 3) -> list[dict[str, Any]]:
        cur = self.conn.execute(
            "SELECT * FROM generated_news WHERE ticker = ? AND status = 'published' "
            "ORDER BY published_at DESC LIMIT ?",
            (ticker, limit),
        )
        return [dict(r) for r in cur.fetchall()]

    def close(self) -> None:
        self.conn.close()
